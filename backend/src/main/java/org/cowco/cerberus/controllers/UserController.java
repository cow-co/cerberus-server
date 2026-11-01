package org.cowco.cerberus.controllers;

import java.util.ArrayList;
import java.util.List;

import org.cowco.cerberus.entities.UserEntity;
import org.cowco.cerberus.entities.responses.UserResponse;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController 
@RequestMapping(path = "/users")
public class UserController {
    @Autowired 
    private UserRepository userRepository;

    @GetMapping
    public List<UserResponse> getUsers() {
        Iterable<UserEntity> accounts = userRepository.findAll();
        List<UserResponse> response = new ArrayList<>();
        accounts.forEach(account -> {
            response.add(new UserResponse(account.getId(), account.getUsername()));
        });
        return response;
    }
}
