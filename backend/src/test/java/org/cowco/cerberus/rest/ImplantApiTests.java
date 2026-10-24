package org.cowco.cerberus.rest;

import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.client.RestTestClient;

@SpringBootTest 
@AutoConfigureMockMvc 
@AutoConfigureRestTestClient
public class ImplantApiTests {
    @Autowired 
    private RestTestClient client;

    @Autowired 
    @MockitoBean 
    private ImplantRepository implantRepository;

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testEmptyImplantList() {
        when(implantRepository.findAll()).thenReturn(new ArrayList<>());
        client
            .get()
            .uri("/implants")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(String.class)
            .isEqualTo("[]");
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testNonEmptyImplantList() {
        List<Implant> expected = List.of(new Implant());
        when(implantRepository.findAll()).thenReturn(expected);
        client
            .get()
            .uri("/implants")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(List.class)
            .isEqualTo(expected);
    }
}
