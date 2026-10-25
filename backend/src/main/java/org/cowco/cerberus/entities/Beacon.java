package org.cowco.cerberus.entities;

public class Beacon {
    private long implantId;
    private String hostname;
    private String ipAddr;
    private int majorVer;
    private int minorVer;

    public Beacon(long implantId, String hostname, String ipAddr, int majorVer, int minorVer) {
        this.implantId = implantId;
        this.hostname = hostname;
        this.ipAddr = ipAddr;
        this.majorVer = majorVer;
        this.minorVer = minorVer;
    }
    
    public long getImplantId() {
        return implantId;
    }
    public void setImplantId(long implantId) {
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
    public int getMajorVer() {
        return majorVer;
    }
    public void setMajorVer(int majorVer) {
        this.majorVer = majorVer;
    }
    public int getMinorVer() {
        return minorVer;
    }
    public void setMinorVer(int minorVer) {
        this.minorVer = minorVer;
    }
}
