package org.cowco.cerberus.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;


@Entity
public class Implant {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String ipAddr;  // TODO Swap to using an actual IP Address type
    private String hostname;
    private int implantMajorVersion;
    private int implantMinorVersion;
    private boolean isActive;

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

    public boolean getIsActive() {
        return isActive;
    }

    public void setIsActive(boolean isActive) {
        this.isActive = isActive;
    }

    @Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((id == null) ? 0 : id.hashCode());
        result = prime * result + ((ipAddr == null) ? 0 : ipAddr.hashCode());
        result = prime * result + ((hostname == null) ? 0 : hostname.hashCode());
        result = prime * result + implantMajorVersion;
        result = prime * result + implantMinorVersion;
        result = prime * result + (isActive ? 1231 : 1237);
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        Implant other = (Implant) obj;
        if (id == null) {
            if (other.id != null) {
                return false;
            }
        } else if (!id.equals(other.id)) {
            return false;
        }
        if (ipAddr == null) {
            if (other.ipAddr != null) {
                return false;
            }
        } else if (!ipAddr.equals(other.ipAddr)) {
            return false;
        }
        if (hostname == null) {
            if (other.hostname != null) {
                return false;
            }
        } else if (!hostname.equals(other.hostname)) {
            return false;
        }
        if (implantMajorVersion != other.implantMajorVersion) {
            return false;
        }
        if (implantMinorVersion != other.implantMinorVersion) {
            return false;
        }
        if (isActive != other.isActive) {
            return false;
        }
        return true;
    }

    
}