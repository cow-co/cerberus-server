package org.cowco.cerberus.controllers;

import org.cowco.cerberus.entities.UserEntity;
import org.cowco.cerberus.entities.requests.AuthenticationRequest;
import org.cowco.cerberus.entities.responses.LoginResponse;
import org.cowco.cerberus.middleware.CerberusAuthenticationManager;
import org.cowco.cerberus.middleware.CerberusUserDetailsService;
import org.cowco.cerberus.middleware.JwtManager;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.http.HttpStatusCode;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping(path = "/auth")
public class AuthController {
    private final Logger logger = LogManager.getLogger(getClass());

    @Autowired 
    private CerberusUserDetailsService userDetailsService;
    @Autowired 
    private CerberusAuthenticationManager authManager;
    @Autowired 
    private JwtManager jwtManager;

    @PostMapping
    public LoginResponse login(@RequestBody AuthenticationRequest authRequest) {
        try {
            authManager.authenticate(new UsernamePasswordAuthenticationToken(authRequest.getUsername(), authRequest.getPassword()));
            final UserEntity userEntity = (UserEntity)userDetailsService.loadUserByUsername(authRequest.getUsername());
            final String jwt = jwtManager.generateJWT(userEntity);
            return new LoginResponse(jwt);
        } catch (DisabledException ex) {
            logger.warn("User is locked out!");
            throw new ResponseStatusException(HttpStatusCode.valueOf(401), "Locked Out!");
        } catch (BadCredentialsException | UsernameNotFoundException ex) {
            logger.warn("Could not authenticate user!");
            throw new ResponseStatusException(HttpStatusCode.valueOf(401), "Incorrect Credentials!");
        }
    }
}
