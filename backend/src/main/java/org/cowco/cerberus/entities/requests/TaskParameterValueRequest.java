package org.cowco.cerberus.entities.requests;

public class TaskParameterValueRequest {
    private Long paramId;
    private String stringValue;
    
    public TaskParameterValueRequest() {
    }

    public TaskParameterValueRequest(Long paramId, String stringValue) {
        this.paramId = paramId;
        this.stringValue = stringValue;
    }

    public Long getParamId() {
        return paramId;
    }

    public void setParamId(Long paramId) {
        this.paramId = paramId;
    }

    public String getStringValue() {
        return stringValue;
    }

    public void setStringValue(String stringValue) {
        this.stringValue = stringValue;
    }
    
    
}
