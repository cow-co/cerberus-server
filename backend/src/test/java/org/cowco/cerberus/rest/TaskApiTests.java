package org.cowco.cerberus.rest;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.Task;
import org.cowco.cerberus.entities.TaskType;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.cowco.cerberus.repositories.TaskParameterRepository;
import org.cowco.cerberus.repositories.TaskRepository;
import org.cowco.cerberus.repositories.TaskTypeRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;

@SpringBootTest 
@AutoConfigureMockMvc 
@AutoConfigureRestTestClient
public class TaskApiTests {
    Logger LOGGER = LogManager.getLogger(getClass());
    
    @Autowired 
    private MockMvc mvc;

    @Autowired 
    @MockitoBean 
    private TaskTypeRepository taskTypeRepository;
    @Autowired 
    @MockitoBean 
    private TaskParameterRepository taskParameterRepository;
    @Autowired 
    @MockitoBean 
    private TaskRepository taskRepository;
    @Autowired 
    @MockitoBean 
    private ImplantRepository implantRepository;


    @Test 
    @WithMockUser(roles = "ADMIN")
    void testNoTaskFound() throws Exception {
        when(taskRepository.findById(1L)).thenReturn(Optional.empty());
        mvc.perform(get("/tasks/1"))
            .andExpect(status().isNotFound());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskFound() throws Exception {
        Task task = new Task();
        task.setTaskType(new TaskType());
        task.setId(1L);
        task.setHasBeenSent(true);
        when(taskRepository.findById(1L)).thenReturn(Optional.of(task));

        mvc.perform(get("/tasks/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.hasBeenSent").value(true));
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskCreateTaskTypeNotFound() throws Exception {
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.empty());
        mvc.perform(post("/tasks").contentType(MediaType.APPLICATION_JSON).content("""
            {"typeId": 1, "implantId": 1, "params": []}
        """).with(csrf()))
            .andExpect(status().isNotFound());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskCreateImplantNotFound() throws Exception {
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.of(new TaskType()));
        when(implantRepository.findById(1L)).thenReturn(Optional.empty());
        mvc.perform(post("/tasks").contentType(MediaType.APPLICATION_JSON).content("""
            {"typeId": 1, "implantId": 1, "params": []}
        """).with(csrf()))
            .andExpect(status().isNotFound());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskCreate() throws Exception {
        Task task = new Task();
        task.setTaskType(new TaskType());
        task.setId(1L);
        when(taskRepository.save(any())).thenReturn(task);
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.of(new TaskType()));
        when(implantRepository.findById(1L)).thenReturn(Optional.of(new Implant()));

        mvc.perform(post("/tasks").contentType(MediaType.APPLICATION_JSON).content("""
            {"typeId": 1, "implantId": 1, "params": []}
        """).with(csrf()))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1));
    }

    @Test 
    void testAuthRequired() throws Exception {
        mvc.perform(get("/tasks"))
            .andExpect(status().isUnauthorized());
        
        mvc.perform(get("/tasks/1"))
            .andExpect(status().isUnauthorized());

        mvc.perform(post("/tasks").with(csrf()))
            .andExpect(status().isUnauthorized());
    }

    @Test 
    void testAntiCSRFRequired() throws Exception {
        mvc.perform(post("/tasks").with(csrf().useInvalidToken()))
            .andExpect(status().isForbidden());
    }
}
