package org.cowco.cerberus.controllers;

import org.cowco.cerberus.entities.requests.AuthenticationRequest;
import org.cowco.cerberus.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "/auth")
public class AuthController {
    @Autowired 
    private UserRepository userRepository;

    @PostMapping
    public String login(@RequestBody AuthenticationRequest authRequest) {
        
    }
}
