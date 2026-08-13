from tools.semgrep_tool import SemgrepTool


code = """
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;

public class Test {

    public void search(Connection connection, String username)
            throws Exception {

        Statement statement = connection.createStatement();

        String query = "SELECT * FROM users WHERE name = '" + username + "'";

        ResultSet result = statement.executeQuery(query);
    }
}
"""


result = SemgrepTool.scan(code, "java")

print(result)