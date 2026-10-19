package org.cowco.cerberus.rest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.client.RestTestClient;

@SpringBootTest
@AutoConfigureRestTestClient 
public class ImplantEndpointTests {
    @Autowired 
    private RestTestClient restTestClient;

    @Test 
    void listAllImplants_ShouldReturnNone() {
        restTestClient.get().uri("/implants").exchange().expectBody().jsonPath("_embedded.implants").isEmpty();
    }
}
