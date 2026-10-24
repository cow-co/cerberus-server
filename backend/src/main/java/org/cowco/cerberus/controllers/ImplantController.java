package org.cowco.cerberus.controllers;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jakarta.websocket.server.PathParam;

@RestController
@RequestMapping("implants")
public class ImplantController {
    @Autowired 
    private ImplantRepository implantRepository;

    @GetMapping(produces = "application/json")
    public Iterable<Implant> getImplants() {
        return implantRepository.findAll();
    }

    @GetMapping(path="/{id}", produces = "application/json")
    public Implant getImplantById(@PathVariable long id) {
        // TODO Raise exception if not found
        Optional<Implant> maybeImplant = implantRepository.findById(id);
        return maybeImplant.get();
    }

    @GetMapping(path="/search", produces = "application/json")
    public Iterable<Implant> searchForImplant(
        @PathParam("hostname") String hostname, 
        @PathParam("isActive") Boolean isActive, 
        @PathParam("ipAddr") String ipAddr
    ) {
        Set<Implant> foundImplants = new HashSet<>();
        
        if (hostname != null) {
            List<Implant> hostnameMatched = implantRepository.findByHostname(hostname);
            foundImplants.addAll(hostnameMatched);
        } if (isActive != null) {
            List<Implant> isActiveMatched = implantRepository.findByIsActive(isActive);
            foundImplants.addAll(isActiveMatched);
        } if (ipAddr != null) {
            List<Implant> ipMatched = implantRepository.findByIpAddr(ipAddr);
            foundImplants.addAll(ipMatched);
        }

        return foundImplants;
    }
}
