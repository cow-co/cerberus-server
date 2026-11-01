package org.cowco.cerberus.config;

import org.cowco.cerberus.entities.UserEntity;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component 
public class InitialAdminLoader {
    @Autowired 
    private UserRepository userRepository;
    @Autowired 
    private PasswordEncoder passwordEncoder;

    @Value("${initial.admin.username:initadmin}")
    private String initialAdminName;
    @Value("${initial.admin.username:changeme}")
    private String initialAdminPassword;

    public void load() {
        userRepository.save(new UserEntity(initialAdminName, passwordEncoder.encode(initialAdminPassword), null, 0));
    }
}
