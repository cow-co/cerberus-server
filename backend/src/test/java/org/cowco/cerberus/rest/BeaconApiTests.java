package org.cowco.cerberus.rest;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.booleanThat;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.Task;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.cowco.cerberus.repositories.TaskRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest 
@AutoConfigureMockMvc 
@AutoConfigureRestTestClient
public class BeaconApiTests {
    Logger LOGGER = LogManager.getLogger(getClass());
    
    @Autowired 
    private MockMvc mvc;

    @Autowired 
    @MockitoBean 
    private ImplantRepository implantRepository;

    @Autowired 
    @MockitoBean 
    private TaskRepository taskRepository;

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testBeaconNewImplant() throws Exception {
        when(implantRepository.save(any())).thenReturn(new Implant());
        mvc.perform(
            post("/beacon")
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
        {"hostname": "test", "majorVer": 1, "minorVer": 1}
                """))
        .andExpect(status().isOk());
        verify(implantRepository, times(1)).save(any());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testBeaconExistingImplant() throws Exception {
        when(implantRepository.save(any())).thenReturn(new Implant());
        when(implantRepository.findById(1L)).thenReturn(Optional.of(new Implant()));
        mvc.perform(
            post("/beacon")
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
        {"implantId": 1, "hostname": "test", "majorVer": 1, "minorVer": 1}
                """))
        .andExpect(status().isOk());
        verify(implantRepository, times(1)).save(any());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testBeaconNoTasks() throws Exception {
        when(implantRepository.save(any())).thenReturn(new Implant());
        when(taskRepository.findByImplantAndHasBeenSent(any(),any())).thenReturn(List.of());
        when(implantRepository.findById(1L)).thenReturn(Optional.of(new Implant()));
        mvc
            .perform(
                post("/beacon")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
        {"implantId": 1, "hostname": "test", "majorVer": 1, "minorVer": 1}
                """)
            )
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.tasks").isEmpty());
        verify(implantRepository, times(1)).save(any());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testBeaconSomeTasks() throws Exception {
        when(implantRepository.save(any())).thenReturn(new Implant());
        when(taskRepository.findByImplantAndHasBeenSent(any(), any())).thenReturn(List.of(new Task()));
        when(implantRepository.findById(1L)).thenReturn(Optional.of(new Implant()));
        mvc
            .perform(
                post("/beacon")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
        {"implantId": 1, "hostname": "test", "majorVer": 1, "minorVer": 1}
                """)
            )
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.tasks").isNotEmpty());
        verify(implantRepository, times(1)).save(any());
        verify(taskRepository, times(1)).save(any());
    }
}
