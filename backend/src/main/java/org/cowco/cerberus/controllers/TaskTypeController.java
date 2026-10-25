package org.cowco.cerberus.controllers;

import org.cowco.cerberus.entities.TaskType;
import org.cowco.cerberus.repositories.TaskTypeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("task-types")
public class TaskTypeController {
    @Autowired 
    private TaskTypeRepository taskTypeRepository;

    @GetMapping(produces = "application/json")
    public Iterable<TaskType> getTaskTypes() {
        return taskTypeRepository.findAll();
    }
}
