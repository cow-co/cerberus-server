package org.cowco.cerberus.entities.requests;


import java.util.List;

public class TaskTypeRequest {
    private String taskName;
    private List<TaskParameterRequest> params;
    
    public TaskTypeRequest() {
    }

    public TaskTypeRequest(String taskName, List<TaskParameterRequest> params) {
        this.taskName = taskName;
        this.params = params;
    }
    
    public String getTaskName() {
        return taskName;
    }
    public void setTaskName(String taskName) {
        this.taskName = taskName;
    }
    public List<TaskParameterRequest> getParams() {
        return params;
    }
    public void setParams(List<TaskParameterRequest> params) {
        this.params = params;
    }
    
    
}
