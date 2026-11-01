package org.cowco.cerberus.middleware;

import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.UserEntity;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service 
public class CerberusUserDetailsService implements UserDetailsService {
    private final Logger logger = LogManager.getLogger(getClass());
    
    @Autowired 
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        logger.info("Finding user with name %s".formatted(username));
        Optional<UserEntity> maybeUser = userRepository.findByUsername(username);
        if (maybeUser.isEmpty()) {
            throw new UsernameNotFoundException("Incorrect credentials!");
        }
        return maybeUser.get();
    }

    public UserDetails loadUserById(String id) throws UsernameNotFoundException {
        logger.info("Finding user with ID %s".formatted(id));
        Optional<UserEntity> maybeUser = userRepository.findById(Long.parseLong(id));
        if (maybeUser.isEmpty()) {
            throw new UsernameNotFoundException("Incorrect credentials!");
        }
        return maybeUser.get();
    }

    public long getCountOfUsers() {
        return userRepository.count();
    }
}
