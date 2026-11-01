package org.cowco.cerberus.middleware;

import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.UserEntity;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service 
public class CerberusUserDetailsService implements UserDetailsService {
    private final Logger logger = LogManager.getLogger(getClass());
    @Autowired 
    private UserRepository userRepository;
    @Value("${initial.admin.username:initadmin}")
    private String initialAdminName;
    // FIXME Use a proper env var password
    // TODO Initial admin should be seeded into the database on startup (then deactivated once a new admin is created)

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        logger.info("Finding user with name %s".formatted(username));
        if (getCountOfUsers() > 0) {
            Optional<UserEntity> maybeUser = userRepository.findByUsername(username);
            if (maybeUser.isEmpty()) {
                throw new UsernameNotFoundException("Incorrect credentials!");
            }
            return maybeUser.get();
        } else {
            logger.info("Checking initial admin (which is %s)".formatted(initialAdminName));
            if (username.equals(initialAdminName)) {
                return new UserEntity(initialAdminName, "testing", null, 0);
            } else {
                throw new UsernameNotFoundException("Incorrect credentials!");
            }
        }
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
