package org.cowco.cerberus.repositories;

import org.cowco.cerberus.entities.TaskParameterValue;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface TaskParameterValueRepository extends PagingAndSortingRepository<TaskParameterValue, Long>, CrudRepository<TaskParameterValue, Long> {
    
}
