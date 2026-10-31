package org.cowco.cerberus.entities.responses;

import java.util.List;

import org.cowco.cerberus.entities.Task;

public class BeaconResponse {
    private Long implantId;
    private List<Task> tasks;

    public BeaconResponse() {
    }

    public BeaconResponse(Long implantId, List<Task> tasks) {
        this.implantId = implantId;
        this.tasks = tasks;
    }

    public Long getImplantId() {
        return implantId;
    }
    public void setImplantId(Long implantId) {
        this.implantId = implantId;
    }
    public List<Task> getTasks() {
        return tasks;
    }
    public void setTasks(List<Task> tasks) {
        this.tasks = tasks;
    }
}
