package org.cowco.cerberus.repositories;

import java.util.List;

import org.cowco.cerberus.entities.Implant;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jpa.test.autoconfigure.TestEntityManager;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest 
public class ImplantRepositoryTests {
    @Autowired 
    private TestEntityManager entityManager;
    @Autowired 
    private ImplantRepository implantRepository;

    @Test 
    void getByHostname_NoHostnameImplant() {
        Implant imp = new Implant();
        entityManager.persist(imp);
        entityManager.flush();

        List<Implant> returned = implantRepository.findByHostname("test");

        assertThat(returned).hasSize(0);
    }
}
