package org.cowco.cerberus.middleware;

import org.cowco.cerberus.entities.UserEntity;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component 
public class CerberusAuthenticationManager implements AuthenticationManager {
    private final Logger logger = LogManager.getLogger(getClass());

    @Autowired 
    private CerberusUserDetailsService userDetailsService;
    @Autowired 
    private PasswordEncoder passwordEncoder;

    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        try {
            logger.info("Authenticating with username %s".formatted(authentication.getName()));
            UserEntity userEntity = (UserEntity)userDetailsService.loadUserByUsername(authentication.getName());
            if (passwordEncoder.matches(authentication.getCredentials().toString(), userEntity.getPassword())) {
                return authentication;
            } else {
                throw new BadCredentialsException("Invalid Credentials!");
            }
        } catch (UsernameNotFoundException ex) {
            logger.warn("Username %s does not exist!".formatted(authentication.getName()));
            throw new BadCredentialsException("Invalid Credentials!");
        }
    }
}
