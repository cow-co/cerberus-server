package org.cowco.cerberus.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.Task;
import org.cowco.cerberus.entities.TaskParameter;
import org.cowco.cerberus.entities.TaskParameterValue;
import org.cowco.cerberus.entities.TaskType;
import org.cowco.cerberus.entities.requests.TaskRequest;
import org.cowco.cerberus.entities.requests.TaskTypeRequest;
import org.cowco.cerberus.repositories.ImplantRepository;
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
    @Autowired 
    private ImplantRepository implantRepository;

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
    public Task createTask(@RequestBody TaskRequest task) {
        Optional<TaskType> maybeTT = taskTypeRepository.findById(task.getTypeId());
        if (maybeTT.isEmpty()) {
            throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find that task type!");
        }
        Optional<Implant> maybeImp = implantRepository.findById(task.getImplantId());
        if (maybeImp.isEmpty()) {
            throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find that implant!");
        }


        List<TaskParameterValue> paramValues = new ArrayList<>();
        task.getParams().forEach(param -> {
            Optional<TaskParameter> maybePar = taskParameterRepository.findById(param.getParamId());
            if (maybePar.isEmpty()) {
                throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find that parameter type!");
            }
            paramValues.add(taskParameterValueRepository.save(
                new TaskParameterValue(
                    param.getParamId(), 
                    maybePar.get().getType(), 
                    param.getStringValue()
                )
            ));
        });

        return taskRepository.save(new Task(
            maybeTT.get(),
            false,
            paramValues,
            maybeImp.get()
        ));
    }

    @DeleteMapping(path = "/{id}")
    public void deleteTask(@PathVariable Long id) {
        taskRepository.deleteById(id);
    }

    @PatchMapping(path = "/{id}", produces = "application/json")
    public Task updateTask(@PathVariable Long id, @RequestBody TaskRequest request) {
        // XXX How much do we want to allow the user to modify a task? Versus just making them delete and re-create?
        return new Task();
    }
}
