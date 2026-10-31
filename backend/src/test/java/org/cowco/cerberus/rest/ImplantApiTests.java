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
    @WithMockUser(roles = "ADMIN")
    void testGetsById() {
        Implant imp = new Implant();
        imp.setHostname("test");
        when(implantRepository.findById(1L)).thenReturn(Optional.of(imp));
        client
            .get()
            .uri("/implants/1")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(Implant.class)
            .value(implant -> assertEquals(imp, implant));
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testGetsByIdNonExistent() {
        when(implantRepository.findById(1L)).thenReturn(Optional.empty());
        client
            .get()
            .uri("/implants/1")
            .exchange()
            .expectStatus()
            .isNotFound();
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testSearchesBySingleFactors() {
        Implant imp = new Implant();
        imp.setIsActive(true);
        List<Implant> expected = List.of(imp);
        when(implantRepository.findAll()).thenReturn(expected);
        when(implantRepository.findByIsActive(true)).thenReturn(expected);
        client
            .get()
            .uri("/implants/search?isActive=true")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));

        imp.setHostname("test");
        when(implantRepository.findByHostname("test")).thenReturn(expected);
        client
            .get()
            .uri("/implants/search?hostname=test")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));

        imp.setIPAddr("127.0.0.1");
        when(implantRepository.findByIpAddr("127.0.0.1")).thenReturn(expected);
        client
            .get()
            .uri("/implants/search?ipAddr=127.0.0.1")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));

        imp.setImplantMajorVersion(1);
        when(implantRepository.findByImplantMajorVersion(1)).thenReturn(expected);
        client
            .get()
            .uri("/implants/search?majorVersion=1")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));

        imp.setImplantMinorVersion(2);
        when(implantRepository.findByImplantMinorVersion(2)).thenReturn(expected);
        client
            .get()
            .uri("/implants/search?minorVersion=2")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testSearchesByAllFactors() {
        Implant imp1 = new Implant(
            "127.0.0.1",
            "test",
            1,
            2,
            true
        );
        Implant imp2 = new Implant();
        imp2.setIsActive(true);
        Implant imp3 = new Implant();
        imp3.setHostname("test");
        Implant imp4 = new Implant();
        imp4.setIPAddr("127.0.0.1");
        Implant imp5 = new Implant();
        imp5.setImplantMajorVersion(1);
        Implant imp6 = new Implant();
        imp6.setImplantMinorVersion(1);

        List<Implant> expected = List.of(imp1);
        List<Implant> response1 = List.of(imp1, imp2);
        List<Implant> response2 = List.of(imp1, imp3);
        List<Implant> response3 = List.of(imp1, imp4);
        List<Implant> response4 = List.of(imp1, imp5);
        List<Implant> response5 = List.of(imp1, imp6);
        List<Implant> responseAll = List.of(imp1, imp2, imp3, imp4, imp5, imp6);
        when(implantRepository.findAll()).thenReturn(responseAll);
        
        when(implantRepository.findByIsActive(true)).thenReturn(response1);
        when(implantRepository.findByHostname("test")).thenReturn(response2);
        when(implantRepository.findByIpAddr("127.0.0.1")).thenReturn(response3);
        when(implantRepository.findByImplantMajorVersion(1)).thenReturn(response4);
        when(implantRepository.findByImplantMinorVersion(1)).thenReturn(response5);
        
        client
            .get()
            .uri("/implants/search?isActive=true&hostname=test&ipAddr=127.0.0.1&majorVer=1&minorVer=1")
            .exchange()
            .expectStatus()
            .isOk()
            .expectBody(new ParameterizedTypeReference<List<Implant>>(){})
            .value(implants -> assertEquals(expected, implants));
    }

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
        client
            .get()
            .uri("/implants/search?isActive=true")
            .exchange()
            .expectStatus()
            .isUnauthorized();
    }
}
