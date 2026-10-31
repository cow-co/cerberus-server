package org.cowco.cerberus.rest;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.requests.Beacon;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.cowco.cerberus.repositories.TaskRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.client.RestTestClient;

@SpringBootTest 
@AutoConfigureMockMvc 
@AutoConfigureRestTestClient
public class BeaconApiTests {
    // TODO Fill these out
    Logger LOGGER = LogManager.getLogger(getClass());
    
    @Autowired 
    private RestTestClient client;

    @Autowired 
    @MockitoBean 
    private ImplantRepository implantRepository;

    @Autowired 
    @MockitoBean 
    private TaskRepository taskRepository;
}
