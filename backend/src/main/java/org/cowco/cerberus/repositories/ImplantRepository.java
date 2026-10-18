package org.cowco.cerberus.repositories;

import java.util.List;

import org.cowco.cerberus.entities.Implant;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource(collectionResourceRel = "implants", path = "implants")
public interface ImplantRepository extends PagingAndSortingRepository<Implant, Long>, CrudRepository<Implant, Long> {
    List<Implant> findByHostname(@Param("hostname") String hostname);
}
