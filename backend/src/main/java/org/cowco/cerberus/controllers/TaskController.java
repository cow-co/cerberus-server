package org.cowco.cerberus.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.cowco.cerberus.entities.Task;
import org.cowco.cerberus.entities.TaskParameter;
import org.cowco.cerberus.entities.TaskType;
import org.cowco.cerberus.entities.requests.TaskTypeRequest;
import org.cowco.cerberus.repositories.TaskParameterRepository;
import org.cowco.cerberus.repositories.TaskParameterValueRepository;
import org.cowco.cerberus.repositories.TaskRepository;
import org.cowco.cerberus.repositories.TaskTypeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatusCode;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("tasks")
public class TaskController {
    @Autowired 
    private TaskRepository taskRepository;
    @Autowired 
    private TaskTypeRepository taskTypeRepository;
    @Autowired 
    private TaskParameterRepository taskParameterRepository;
    @Autowired 
    private TaskParameterValueRepository taskParameterValueRepository;

    @GetMapping(produces = "application/json")
    public Iterable<Task> getTasks() {
        return taskRepository.findAll();
    }

    @GetMapping(path = "/{id}", produces = "application/json")
    public Task getTask(@PathVariable Long id) {
        Optional<Task> maybeTask = taskRepository.findById(id);
        if (maybeTask.isEmpty()) {
            throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find task with that ID!");
        }
        return maybeTask.get();
    }

    @PostMapping (produces = "application/json")
    public TaskType createTask(@RequestBody TaskTypeRequest taskType) {
        
    }

    @DeleteMapping(path = "/{id}")
    public void deleteTask(@PathVariable Long id) {
        taskRepository.deleteById(id);
    }

    @PatchMapping(path = "/{id}", produces = "application/json")
    public TaskType updateTask(@PathVariable Long id, @RequestBody TaskTypeRequest request) {
        
    }
}
