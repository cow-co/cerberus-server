package org.cowco.cerberus.entities;

import java.util.List;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OneToOne;

@Entity 
public class Task {
    @Id 
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @OneToOne 
    @JoinColumn(name = "type_id")
    private TaskType taskType;
    private boolean hasBeenSent;

    @OneToMany(mappedBy = "task", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<TaskParameterValue> params;

    public Task() {
    }

    public Task(TaskType taskType, boolean hasBeenSent, List<TaskParameterValue> params) {
        this.taskType = taskType;
        this.hasBeenSent = hasBeenSent;
        this.params = params;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public TaskType getTaskType() {
        return taskType;
    }

    public void setTaskType(TaskType taskType) {
        this.taskType = taskType;
    }

    public boolean isHasBeenSent() {
        return hasBeenSent;
    }

    public void setHasBeenSent(boolean hasBeenSent) {
        this.hasBeenSent = hasBeenSent;
    }

    public List<TaskParameterValue> getParams() {
        return params;
    }

    public void setParams(List<TaskParameterValue> params) {
        this.params = params;
    }

    
}
