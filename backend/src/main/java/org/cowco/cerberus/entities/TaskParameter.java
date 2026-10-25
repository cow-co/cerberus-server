package org.cowco.cerberus.entities;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;



public class TaskParameter {
    @Id 
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String name;
    private TaskParamType type;
    
    public TaskParameter() {
    }

    public TaskParameter(String name, TaskParamType type) {
        this.name = name;
        this.type = type;
    }
    
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
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
