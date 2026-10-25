package org.cowco.cerberus.entities;

public class Beacon {
    private Long implantId;
    private String hostname;
    private String ipAddr;
    private Integer majorVer;
    private Integer minorVer;

    public Beacon() {
    }

    public Beacon(Long implantId, String hostname, String ipAddr, Integer majorVer, Integer minorVer) {
        this.implantId = implantId;
        this.hostname = hostname;
        this.ipAddr = ipAddr;
        this.majorVer = majorVer;
        this.minorVer = minorVer;
    }
    
    public Long getImplantId() {
        return implantId;
    }
    public void setImplantId(Long implantId) {
        this.implantId = implantId;
    }
    public String getHostname() {
        return hostname;
    }
    public void setHostname(String hostname) {
        this.hostname = hostname;
    }
    public String getIpAddr() {
        return ipAddr;
    }
    public void setIpAddr(String ipAddr) {
        this.ipAddr = ipAddr;
    }
    public Integer getMajorVer() {
        return majorVer;
    }
    public void setMajorVer(Integer majorVer) {
        this.majorVer = majorVer;
    }
    public Integer getMinorVer() {
        return minorVer;
    }
    public void setMinorVer(Integer minorVer) {
        this.minorVer = minorVer;
    }
}
