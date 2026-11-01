package org.cowco.cerberus.middleware;

import java.time.Instant;

import org.cowco.cerberus.entities.UserEntity;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;

@Component 
public class JwtManager {
    @Value("${jwt.expiry:3600000}")
    private long jwtExpiryMillis;
    @Value("${jwt.secret:test}")
    private String jwtSecret;
    private Algorithm alg;

    public JwtManager() {
        alg = Algorithm.HMAC256(jwtSecret);
    }

    public String generateJWT(UserEntity user) {
        final Instant issued = Instant.now();
        final Instant expires = issued.plusMillis(jwtExpiryMillis);
        return JWT
            .create()
            .withSubject(user.getId().toString())
            .withIssuer("CERBERUS")
            .withIssuedAt(issued)
            .withExpiresAt(expires)
            .sign(alg);
    }

    /**
     * Verifies and decodes the JWT
     * @param jwt
     * @return The JWT subject (user ID, in string form)
     */
    public String verifyJWT(String jwt) {
        DecodedJWT decoded = JWT.require(alg).build().verify(jwt);
        return decoded.getSubject();
    }
}
