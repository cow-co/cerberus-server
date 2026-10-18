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

    @Test 
    void getByHostname_OneImplantWithHostnameNoMatch() {
        Implant imp = new Implant();
        imp.setHostname("test.name");
        entityManager.persist(imp);
        entityManager.flush();

        List<Implant> returned = implantRepository.findByHostname("test");

        assertThat(returned).hasSize(0);
    }

    @Test 
    void getByHostname_OneImplantWithHostnameMatched() {
        Implant imp = new Implant();
        imp.setHostname("test.name");
        entityManager.persist(imp);
        entityManager.flush();

        List<Implant> returned = implantRepository.findByHostname("test.name");

        assertThat(returned).hasSize(1);
    }

    @Test 
    void getByHostname_MultipleImplantsWithHostnameMatched() {
        Implant imp1 = new Implant();
        imp1.setHostname("test.name");
        Implant imp2 = new Implant();
        imp2.setHostname("test.name");
        Implant imp3 = new Implant();
        imp3.setHostname("test2.name");
        entityManager.persist(imp1);
        entityManager.persist(imp2);
        entityManager.persist(imp3);
        entityManager.flush();

        List<Implant> returned = implantRepository.findByHostname("test.name");

        assertThat(returned).hasSize(2);
    }
}
