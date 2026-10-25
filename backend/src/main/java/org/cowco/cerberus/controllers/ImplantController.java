package org.cowco.cerberus.controllers;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

import org.cowco.cerberus.entities.Beacon;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.repositories.ImplantRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatusCode;
import org.springframework.security.web.firewall.RequestRejectedException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

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
        Optional<Implant> maybeImplant = implantRepository.findById(id);
        if (maybeImplant.isEmpty()) {
            throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find an implant with that ID!");
        }
        return maybeImplant.get();
    }

    @GetMapping(path="/search", produces = "application/json")
    public Iterable<Implant> searchForImplant(
        @PathParam("hostname") String hostname, 
        @PathParam("isActive") Boolean isActive, 
        @PathParam("ipAddr") String ipAddr,
        @PathParam("majorVersion") Integer majorVersion,
        @PathParam("minorVersion") Integer minorVersion
    ) {
        Set<Implant> foundImplants = new HashSet<>();
        foundImplants.addAll((List)implantRepository.findAll());
        
        if (hostname != null) {
            List<Implant> hostnameMatched = implantRepository.findByHostname(hostname);
            foundImplants.retainAll(hostnameMatched);
        } if (isActive != null) {
            List<Implant> isActiveMatched = implantRepository.findByIsActive(isActive);
            foundImplants.retainAll(isActiveMatched);
        } if (ipAddr != null) {
            List<Implant> ipMatched = implantRepository.findByIpAddr(ipAddr);
            foundImplants.retainAll(ipMatched);
        } if (majorVersion != null) {
            List<Implant> majorsMatched = implantRepository.findByImplantMajorVersion(majorVersion);
            foundImplants.retainAll(majorsMatched);
        } if (minorVersion != null) {
            List<Implant> minorsMatched = implantRepository.findByImplantMinorVersion(minorVersion);
            foundImplants.retainAll(minorsMatched);
        }

        return foundImplants;
    }

    @PostMapping(path="/beacon", produces = "application/json")
    public void beacon(@RequestBody Beacon beacon) {
        // The first beacon from an implant will have no ID
        if (beacon.getImplantId() == null) {
            Implant newImp = new Implant(
                beacon.getIpAddr(),
                beacon.getHostname(),
                beacon.getMajorVer(),
                beacon.getMinorVer(),
                true
            );
            implantRepository.save(newImp);
        } else {
            Optional<Implant> maybeImplant = implantRepository.findById(beacon.getImplantId());
            if (maybeImplant.isEmpty()) {
                throw new ResponseStatusException(HttpStatusCode.valueOf(404), "Could not find an implant with that ID!");
            }
            Implant imp = maybeImplant.get();
            if (beacon.getHostname() != null) {
                imp.setHostname(beacon.getHostname());
            }
            if (beacon.getIpAddr() != null) {
                imp.setHostname(beacon.getIpAddr());
            }
            if (beacon.getMajorVer() != null) {
                imp.setImplantMajorVersion(beacon.getMajorVer());
            }
            if (beacon.getMinorVer() != null) {
                imp.setImplantMinorVersion(beacon.getMinorVer());
            }
            imp.setIsActive(true);
            implantRepository.save(imp);
        }
    }
}
