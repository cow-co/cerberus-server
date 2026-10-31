package org.cowco.cerberus.entities.requests;


import java.util.List;

public class TaskRequest {
    private Long typeId;
    private Long implantId;
    private List<TaskParameterValueRequest> params;
    
    public TaskRequest() {
    }
    
    public TaskRequest(Long typeId, Long implantId, List<TaskParameterValueRequest> params) {
        this.typeId = typeId;
        this.implantId = implantId;
        this.params = params;
    }

    public Long getTypeId() {
        return typeId;
    }

    public void setTypeId(Long typeId) {
        this.typeId = typeId;
    }

    public Long getImplantId() {
        return implantId;
    }

    public void setImplantId(Long implantId) {
        this.implantId = implantId;
    }

    public List<TaskParameterValueRequest> getParams() {
        return params;
    }

    public void setParams(List<TaskParameterValueRequest> params) {
        this.params = params;
    }
    
    
}
