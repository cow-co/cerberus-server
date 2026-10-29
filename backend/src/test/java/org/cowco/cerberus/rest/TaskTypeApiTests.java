package org.cowco.cerberus.rest;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.TaskType;
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
public class TaskTypeApiTests {
    Logger LOGGER = LogManager.getLogger(getClass());
    
    @Autowired 
    private MockMvc mvc;

    @Autowired 
    @MockitoBean 
    private TaskTypeRepository taskTypeRepository;


    @Test 
    @WithMockUser(roles = "ADMIN")
    void testNoTaskTypeFound() throws Exception {
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.empty());
        mvc.perform(get("/task-types/1"))
            .andExpect(status().isNotFound());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskTypeFound() throws Exception {
        TaskType task = new TaskType();
        task.setTaskTypeName("test");
        task.setId(1L);
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.of(task));

        mvc.perform(get("/task-types/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.taskTypeName").value("test"));
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskTypeUpdateNotFound() throws Exception {
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.empty());
        mvc.perform(patch("/task-types/1").contentType(MediaType.APPLICATION_JSON).content("""
            {"taskTypeName": "test", "params": []}
        """).with(csrf()))
            .andExpect(status().isNotFound());
    }

    @Test 
    @WithMockUser(roles = "ADMIN")
    void testTaskTypeUpdate() throws Exception {
        TaskType tt = new TaskType();
        tt.setId(1L);
        tt.setTaskTypeName("test");
        when(taskTypeRepository.findById(1L)).thenReturn(Optional.of(tt));
        when(taskTypeRepository.save(any())).thenReturn(tt);

        mvc.perform(patch("/task-types/1").contentType(MediaType.APPLICATION_JSON).content("""
            {"taskTypeName": "test", "params": []}
        """).with(csrf()))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1));
    }

    @Test 
    void testAuthRequired() throws Exception {
        mvc.perform(get("/task-types"))
            .andExpect(status().isUnauthorized());
        
        mvc.perform(get("/task-types/1"))
            .andExpect(status().isUnauthorized());

        mvc.perform(post("/task-types").with(csrf()))
            .andExpect(status().isUnauthorized());
    }

    @Test 
    void testAntiCSRFRequired() throws Exception {
        mvc.perform(post("/task-types").with(csrf().useInvalidToken()))
            .andExpect(status().isForbidden());
        mvc.perform(patch("/task-types/1").with(csrf().useInvalidToken()))
            .andExpect(status().isForbidden());
    }
}
