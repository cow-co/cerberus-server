package org.cowco.cerberus.repositories;

import java.util.List;

import org.cowco.cerberus.entities.User;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;

public interface UserRepository extends PagingAndSortingRepository<User, Long>, CrudRepository<User, Long> {
    List<User> findByUsername(String username);
}
