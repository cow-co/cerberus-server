package org.cowco.cerberus.rest;

import static org.mockito.Mockito.when;

import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.repositories.TaskTypeRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.client.RestTestClient;

// @SpringBootTest 
// @AutoConfigureMockMvc 
// @AutoConfigureRestTestClient
// public class TaskTypeApiTests {
//     Logger LOGGER = LogManager.getLogger(getClass());
    
//     @Autowired 
//     private RestTestClient client;

//     @Autowired 
//     @MockitoBean 
//     private TaskTypeRepository taskTypeRepository;


//     @Test 
//     @WithMockUser(roles = "ADMIN")
//     void testNoTaskTypeFound() {
//         when(taskTypeRepository.findById(1L)).thenReturn(Optional.empty());
//         client
//             .get()
//             .uri("/task-types/1")
//             .exchange()
//             .expectStatus()
//             .isNotFound();
//     }

//     @Test 
//     void testAuthRequired() {
//         client
//             .get()
//             .uri("/task-types/1")
//             .exchange()
//             .expectStatus()
//             .isForbidden();
        
//         client
//             .get()
//             .uri("/task-types")
//             .exchange()
//             .expectStatus()
//             .isForbidden();

//         client
//             .post()
//             .uri("/task-types")
//             .exchange()
//             .expectStatus()
//             .isForbidden();
//     }
// }
