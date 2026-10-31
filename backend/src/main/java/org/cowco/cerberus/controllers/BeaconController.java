package org.cowco.cerberus.controllers;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatusCode;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.Task;
import org.cowco.cerberus.entities.requests.Beacon;
import org.cowco.cerberus.entities.responses.BeaconResponse;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.cowco.cerberus.repositories.TaskRepository;

@RestController
public class BeaconController {
    Logger LOGGER = LogManager.getLogger(getClass());

    @Autowired 
    private ImplantRepository implantRepository;
    @Autowired 
    private TaskRepository taskRepository;

    @PostMapping(path="/beacon", produces = "application/json")
    public BeaconResponse beacon(@RequestBody Beacon beacon) {
        Implant imp;
        // The first beacon from an implant will have no ID
        if (beacon.getImplantId() == null) {
            imp = new Implant();
            imp.setHostname(beacon.getHostname());
            imp.setIpAddr(beacon.getHostname());
            imp.setImplantMajorVersion(beacon.getMajorVer());
            imp.setImplantMinorVersion(beacon.getMinorVer());
            imp.setIsActive(true);
            imp = implantRepository.save(imp);
        } else {
            Optional<Implant> maybeImplant = implantRepository.findById(beacon.getImplantId());
            if (maybeImplant.isEmpty()) {
                LOGGER.warn("Could not find implant with ID %s from beacon".formatted(beacon.getImplantId()));
                throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find an implant with that ID!");
            }
            imp = maybeImplant.get();
            if (beacon.getHostname() != null) {
                imp.setHostname(beacon.getHostname());
            }
            if (beacon.getIpAddr() != null) {
                imp.setHostname(beacon.getIpAddr());
            }
            imp.setImplantMajorVersion(beacon.getMajorVer());
            imp.setImplantMinorVersion(beacon.getMinorVer());
            imp.setIsActive(true);
            imp = implantRepository.save(imp);
        }

        beacon.getSuccessfulTasks().forEach(taskId -> {
            Optional<Task> maybeCompleted = taskRepository.findById(taskId);
            if (maybeCompleted.isEmpty()) {
                LOGGER.warn("Task not found, could not set to successful");
            } else {
                Task completed = maybeCompleted.get();
                completed.setSuccess(true);
                taskRepository.save(completed);
            }
        });

        beacon.getFailedTasks().forEach(taskId -> {
            Optional<Task> maybeCompleted = taskRepository.findById(taskId);
            if (maybeCompleted.isEmpty()) {
                LOGGER.warn("Task not found, could not set to failed");
            } else {
                Task completed = maybeCompleted.get();
                completed.setSuccess(false);
                taskRepository.save(completed);
            }
        });

        List<Task> tasksForImplant = taskRepository.findByImplantAndHasBeenSent(imp, false);
        tasksForImplant.forEach(task -> {
            task.setHasBeenSent(true);
            taskRepository.save(task);
        });
        return new BeaconResponse(imp.getId(), tasksForImplant);
    }
}
