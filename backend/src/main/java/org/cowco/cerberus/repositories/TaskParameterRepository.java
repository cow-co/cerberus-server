package org.cowco.cerberus.repositories;

import org.cowco.cerberus.entities.TaskParameter;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface TaskParameterRepository extends PagingAndSortingRepository<TaskParameter, Long>, CrudRepository<TaskParameter, Long> {
    
}
