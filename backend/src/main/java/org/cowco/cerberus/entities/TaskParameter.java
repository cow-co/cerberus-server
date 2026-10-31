package org.cowco.cerberus.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class TaskParameter {
    @Id 
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String name;
    private TaskParamType type;

    // TODO There should be a unqiue constraint on (name, taskType_id)

    @ManyToOne
    @JoinColumn(name = "taskType_id")
    private TaskType taskType;
    
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
