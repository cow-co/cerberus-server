package org.cowco.cerberus.entities.requests;

import org.cowco.cerberus.entities.TaskParamType;

public class TaskParameterRequest {
    private String name;
    private TaskParamType type;
    
    public TaskParameterRequest() {
    }

    public TaskParameterRequest(String name, TaskParamType type) {
        this.name = name;
        this.type = type;
    }
    
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public TaskParamType getType() {
        return type;
    }
    public void setType(TaskParamType type) {
        this.type = type;
    }

    
}
