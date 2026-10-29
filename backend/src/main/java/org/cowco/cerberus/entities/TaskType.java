package org.cowco.cerberus.entities;


import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;

@Entity
public class TaskType {
    @Id 
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @Column(unique = true)
    private String taskTypeName;

    @OneToMany(mappedBy = "taskType", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<TaskParameter> params;
    
    public TaskType() {
    }

    public TaskType(String taskName, List<TaskParameter> params) {
        this.taskTypeName = taskName;
        this.params = params;
    }
    
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public String getTaskTypeName() {
        return taskTypeName;
    }
    public void setTaskTypeName(String taskTypeName) {
        this.taskTypeName = taskTypeName;
    }
    public List<TaskParameter> getParams() {
        return params;
    }
    public void setParams(List<TaskParameter> params) {
        this.params = params;
    }
    
    
}
