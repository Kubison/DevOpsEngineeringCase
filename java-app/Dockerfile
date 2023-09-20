FROM  amazoncorretto:11 as build
WORKDIR /app
COPY ./ /app/
RUN chmod +x mvnw
RUN ./mvnw package
FROM amazoncorretto:11-alpine-jdk
WORKDIR /app
COPY --from=build /app/target/app-0.0.1-SNAPSHOT.jar ./
EXPOSE 9001/tcp
CMD [ "java", "-jar", "app-0.0.1-SNAPSHOT.jar" ]