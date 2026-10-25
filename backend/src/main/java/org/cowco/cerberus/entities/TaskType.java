package org.cowco.cerberus.entities;


import java.util.List;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

public class TaskType {
    @Id 
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String taskName;
    private List<TaskParameter> params;
    
    public TaskType() {
    }

    public TaskType(String taskName, List<TaskParameter> params) {
        this.taskName = taskName;
        this.params = params;
    }
    
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public String getTaskName() {
        return taskName;
    }
    public void setTaskName(String taskName) {
        this.taskName = taskName;
    }
    public List<TaskParameter> getParams() {
        return params;
    }
    public void setParams(List<TaskParameter> params) {
        this.params = params;
    }
    
    
}
