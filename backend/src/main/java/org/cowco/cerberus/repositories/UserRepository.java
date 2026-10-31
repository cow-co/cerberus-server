package org.cowco.cerberus.repositories;

import java.util.Optional;

import org.cowco.cerberus.entities.UserEntity;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface UserRepository extends PagingAndSortingRepository<UserEntity, Long>, CrudRepository<UserEntity, Long> {
    Optional<UserEntity> findByUsername(String username);
}
