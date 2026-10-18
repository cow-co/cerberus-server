package org.cowco.cerberus.entities;

import org.springframework.data.annotation.Id;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;


@Entity
public class Implant {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;

    private String ipAddr;  // TODO Swap to using an actual IP Address type
    private String hostname;
    private int implantMajorVersion;
    private int implantMinorVersion;

    public String getIPAddr() {
        return ipAddr;
    }

    public void setIPAddr(String ipAddr) {
        this.ipAddr = ipAddr;
    }

    public String getHostname() {
        return hostname;
    }

    public void setHostname(String hostname) {
        this.hostname = hostname;
    }

    public int getImplantMajorVersion() {
        return implantMajorVersion;
    }

    public void setImplantMajorVersion(int implantMajorVersion) {
        this.implantMajorVersion = implantMajorVersion;
    }

    public int getImplantMinorVersion() {
        return implantMinorVersion;
    }

    public void setImplantMinorVersion(int implantMinorVersion) {
        this.implantMinorVersion = implantMinorVersion;
    }
}