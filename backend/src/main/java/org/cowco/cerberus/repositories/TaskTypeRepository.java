package org.cowco.cerberus.repositories;

import java.util.List;

import org.cowco.cerberus.entities.TaskType;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;

public interface TaskTypeRepository extends PagingAndSortingRepository<TaskType, Long>, CrudRepository<TaskType, Long> {
    List<TaskType> findByTaskTypeName(@Param("tasktypename") String taskTypeName);
}
