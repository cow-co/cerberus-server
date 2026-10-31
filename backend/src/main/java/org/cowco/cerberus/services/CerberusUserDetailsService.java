package org.cowco.cerberus.services;

import java.util.ArrayList;
import java.util.Optional;

import org.cowco.cerberus.entities.UserEntity;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service 
public class CerberusUserDetailsService implements UserDetailsService {
    @Autowired 
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Optional<UserEntity> maybeUser = userRepository.findByUsername(username);
        if (maybeUser.isEmpty()) {
            throw new UsernameNotFoundException("Incorrect credentials!");
        }
        return new User(maybeUser.get().getUsername(), maybeUser.get().getHashedPassword(), new ArrayList<>());
    }
}
