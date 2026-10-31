package org.cowco.cerberus.repositories;

import java.util.List;

import org.cowco.cerberus.entities.Implant;
import org.cowco.cerberus.entities.Task;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jpa.test.autoconfigure.TestEntityManager;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Note we don't test auto-generated methods since that should be tested adequately by Spring themselves
 */
@DataJpaTest 
public class TaskRepositoryTests {
    @Autowired 
    private TestEntityManager entityManager;
    @Autowired 
    private TaskRepository taskRepository;
    
    @Test 
    void testGetBySentStatusForImplantNoneForImplant() {
        Task task = new Task();
        Implant imp = new Implant();
        Implant imp2 = new Implant();
        entityManager.persist(imp);
        entityManager.persist(imp2);
        entityManager.flush();
        task.setHasBeenSent(true);
        task.setImplant(imp2);
        entityManager.persist(task);
        entityManager.flush();

        List<Task> returned = taskRepository.findByImplantAndHasBeenSent(imp, true);

        assertThat(returned).hasSize(0);
    }
    
    @Test 
    void testGetBySentStatusForImplantNoneForSentStatus() {
        Task task = new Task();
        Implant imp = new Implant();
        entityManager.persist(imp);
        entityManager.flush();
        task.setHasBeenSent(true);
        task.setImplant(imp);
        entityManager.persist(task);
        entityManager.flush();

        List<Task> returned = taskRepository.findByImplantAndHasBeenSent(imp, false);

        assertThat(returned).hasSize(0);
    }
    
    @Test 
    void testGetBySentStatusForImplant() {
        Task task = new Task();
        Implant imp = new Implant();
        entityManager.persist(imp);
        entityManager.flush();
        task.setHasBeenSent(true);
        task.setImplant(imp);
        entityManager.persist(task);
        entityManager.flush();

        List<Task> returned = taskRepository.findByImplantAndHasBeenSent(imp, true);

        assertThat(returned).hasSize(1);
    }
}
