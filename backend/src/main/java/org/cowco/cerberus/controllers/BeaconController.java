package org.cowco.cerberus.controllers;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatusCode;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import org.cowco.cerberus.entities.Beacon;
import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.repositories.ImplantRepository;

@RestController
public class BeaconController {
    @Autowired 
    private ImplantRepository implantRepository;

    @PostMapping(path="/beacon", produces = "application/json")
    public void beacon(@RequestBody Beacon beacon) {
        // The first beacon from an implant will have no ID
        if (beacon.getImplantId() == null) {
            Implant newImp = new Implant();
            newImp.setHostname(beacon.getHostname());
            newImp.setIPAddr(beacon.getHostname());
            newImp.setImplantMajorVersion(beacon.getMajorVer());
            newImp.setImplantMinorVersion(beacon.getMinorVer());
            newImp.setIsActive(true);
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
