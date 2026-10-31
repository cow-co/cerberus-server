package org.cowco.cerberus.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class TaskParameterValue {
    @Id 
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private Long paramId;
    private TaskParamType type;
    private String stringValue;
    
    @ManyToOne
    @JoinColumn(name = "task_id")
    private Task task;

    public TaskParameterValue() {
    }

    public TaskParameterValue(Long paramId, TaskParamType type, String stringValue) {
        this.paramId = paramId;
        this.type = type;
        this.stringValue = stringValue;
    }
    
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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

    public TaskParamType getType() {
        return type;
    } 

    public void setType(TaskParamType type) {
        this.type = type;
    }
}
