package org.cowco.cerberus.rest;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

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
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.client.RestTestClient;

@SpringBootTest 
@AutoConfigureMockMvc 
@AutoConfigureRestTestClient
public class BeaconApiTests {
    Logger LOGGER = LogManager.getLogger(getClass());
    
    @Autowired 
    private RestTestClient client;

    @Autowired 
    @MockitoBean 
    private ImplantRepository implantRepository;

    @Autowired 
    @MockitoBean 
    private TaskRepository taskRepository;

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testBeaconNewImplant() {
        client
            .post()
            .uri("/beacon")
            .body(new Beacon(null, "test", null, 1, 1))
            .exchange()
            .expectStatus()
            .isOk();
        verify(implantRepository, times(1)).save(any());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testBeaconExistingImplant() {
        when(implantRepository.findById(1L)).thenReturn(Optional.of(new Implant()));
        client
            .post()
            .uri("/beacon")
            .body(new Beacon(1L, "test", null, 1, 1))
            .exchange()
            .expectStatus()
            .isOk();
        verify(implantRepository, times(1)).save(any());
    }

    // TODO Test for empty queue response
    // TODO Test for empty queue response (when there are sent-items in the DB)
    // TODO Non-empty queue response
}
