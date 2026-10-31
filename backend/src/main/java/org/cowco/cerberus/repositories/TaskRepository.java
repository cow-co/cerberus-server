package org.cowco.cerberus.repositories;

import java.util.List;

import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.Task;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;

public interface TaskRepository extends PagingAndSortingRepository<Task, Long>, CrudRepository<Task, Long> {
    List<Task> findByTaskType(@Param("tasktype") String taskType);
    List<Task> findByImplantAndHasBeenSent(@Param("implant") Implant implant, @Param("hasbeensent") Boolean hasBeenSent);
}
