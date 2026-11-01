package org.cowco.cerberus.middleware;

import java.io.IOException;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cowco.cerberus.entities.UserEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetails;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.auth0.jwt.exceptions.JWTVerificationException;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Component 
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private Logger logger = LogManager.getLogger(getClass());

    @Autowired 
    private CerberusUserDetailsService userDetailsService;
    @Autowired 
    private JwtManager jwtManager;

    @Override 
    protected void doFilterInternal(
        HttpServletRequest req,
        HttpServletResponse res,
        FilterChain filterChain
    ) throws ServletException, IOException {
        logger.info("Checking for JWT");
        String authHeader = req.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            try {
                logger.info("Validating JWT");
                String userIdString = jwtManager.verifyJWT(token);
                UserEntity user = (UserEntity)userDetailsService.loadUserById(userIdString);
                UsernamePasswordAuthenticationToken internalToken = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
                internalToken.setDetails(new WebAuthenticationDetails(req));
                SecurityContextHolder.getContext().setAuthentication(internalToken);
            } catch (JWTVerificationException ex) {
                logger.warn("Failed to validate JWT!");
                throw new IOException();
            }
        }
        filterChain.doFilter(req, res);
    }
}
