package org.cowco.cerberus.rest;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.repositories.ImplantRepository;
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
public class ImplantApiTests {
    Logger LOGGER = LogManager.getLogger(getClass());
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
        List<Implant> expected = List.of(new Implant(), new Implant());
        when(implantRepository.findAll()).thenReturn(expected);
        client
            .get()
            .uri("/implants")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testNonEmptyImplantListNonDefaultValues() {
        Implant imp1 = new Implant();
        imp1.setHostname("test");
        Implant imp2 = new Implant();
        imp2.setIPAddr("127.0.0.1");
        Implant imp3 = new Implant();
        imp3.setIsActive(true);
        Implant imp4 = new Implant();
        imp4.setImplantMajorVersion(1);
        Implant imp5 = new Implant();
        imp5.setImplantMinorVersion(2);
        List<Implant> expected = List.of(imp1, imp2, imp3, imp4, imp5);
        when(implantRepository.findAll()).thenReturn(expected);
        client
            .get()
            .uri("/implants")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));
    }

    @Test 
    void testUnauthenticatedUserCannotCallEndpoints() {
        client
            .get()
            .uri("/implants")
            .exchange()
            .expectStatus()
            .isUnauthorized();
        client
            .get()
            .uri("/implants/15")
            .exchange()
            .expectStatus()
            .isUnauthorized();
    }
}
