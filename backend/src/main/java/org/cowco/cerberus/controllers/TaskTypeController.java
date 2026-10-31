package org.cowco.cerberus.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.cowco.cerberus.entities.TaskParameter;
import org.cowco.cerberus.entities.TaskType;
import org.cowco.cerberus.entities.requests.TaskTypeRequest;
import org.cowco.cerberus.repositories.TaskParameterRepository;
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
@RequestMapping("task-types")
public class TaskTypeController {
    @Autowired 
    private TaskTypeRepository taskTypeRepository;
    @Autowired 
    private TaskParameterRepository taskParameterRepository;

    @GetMapping(produces = "application/json")
    public Iterable<TaskType> getTaskTypes() {
        return taskTypeRepository.findAll();
    }

    @GetMapping(path = "/{id}", produces = "application/json")
    public TaskType getTaskType(@PathVariable Long id) {
        Optional<TaskType> maybeTaskType = taskTypeRepository.findById(id);
        if (maybeTaskType.isEmpty()) {
            throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find task type with that ID!");
        }
        return maybeTaskType.get();
    }

    @PostMapping (produces = "application/json")
    public TaskType createTaskType(@RequestBody TaskTypeRequest taskType) {
        List<TaskParameter> createdParams = new ArrayList<>();
        taskType.getParams().forEach(param -> {
            createdParams.add(taskParameterRepository.save(
                new TaskParameter(
                    param.getName(),
                    param.getType()
                )
            ));
        });
        return taskTypeRepository.save(new TaskType(
            taskType.getTaskName(),
            createdParams
        ));
    }

    @DeleteMapping(path = "/{id}")
    public void deleteTaskType(@PathVariable Long id) {
        taskTypeRepository.deleteById(id);
    }

    @PatchMapping(path = "/{id}", produces = "application/json")
    public TaskType updateTaskType(@PathVariable Long id, @RequestBody TaskTypeRequest request) {
        Optional<TaskType> maybeExisting = taskTypeRepository.findById(id);
        if (maybeExisting.isEmpty()) {
            throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Task Type not Found");
        }
        TaskType existing = maybeExisting.get();
        taskTypeRepository.delete(existing);
        List<TaskParameter> createdParams = new ArrayList<>();
        request.getParams().forEach(param -> {
            createdParams.add(taskParameterRepository.save(
                new TaskParameter(
                    param.getName(),
                    param.getType()
                )
            ));
        });
        TaskType newTT = new TaskType(request.getTaskName(), createdParams);
        newTT.setId(id);
        return taskTypeRepository.save(newTT);
    }
}
