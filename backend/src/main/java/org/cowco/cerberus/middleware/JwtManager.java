package org.cowco.cerberus.middleware;

import java.time.Instant;

import org.cowco.cerberus.entities.UserEntity;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;

@Component 
public class JwtManager {
    private static final String ISSUER = "CERBERUS";

    @Value("${jwt.expiry:3600000}")
    private long jwtExpiryMillis;
    @Value("${jwt.secret:test}")
    private String jwtSecret;
    private Algorithm alg;
    private JWTVerifier verifier;

    public String generateJWT(UserEntity user) throws JWTCreationException {
        if (alg == null) {
            alg = Algorithm.HMAC256(jwtSecret);
        }
        final Instant issued = Instant.now();
        final Instant expires = issued.plusMillis(jwtExpiryMillis);
        return JWT
            .create()
            .withSubject(user.getId().toString())
            .withIssuer(ISSUER)
            .withIssuedAt(issued)
            .withExpiresAt(expires)
            .sign(alg);
    }

    /**
     * Verifies and decodes the JWT
     * @param jwt
     * @return The JWT subject (user ID, in string form)
     */
    public String verifyJWT(String jwt) throws JWTVerificationException {
        if (alg == null) {
            alg = Algorithm.HMAC256(jwtSecret);
        }
        if (verifier == null) {
            verifier = JWT.require(alg).withIssuer(ISSUER).build();
        }
        DecodedJWT decoded = verifier.verify(jwt);
        return decoded.getSubject();
    }
}
